const json = (data, status = 200) => new Response(JSON.stringify(data, null, 2), {
  status,
  headers: { "content-type": "application/json; charset=utf-8" }
});

const nowIso = () => new Date().toISOString();

function stateId(env, key = "default") {
  return env.NEXUS_STATE.idFromName(key);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const key = url.searchParams.get("key") || "default";
    const stub = env.NEXUS_STATE.get(stateId(env, key));

    if (url.pathname === "/health") {
      return stub.fetch(new Request(new URL("/state", request.url)));
    }

    if (url.pathname === "/state") {
      return stub.fetch(new Request(new URL("/state", request.url)));
    }

    if (["/task", "/schedule", "/approve", "/run"].includes(url.pathname) && request.method === "POST") {
      const body = await request.json().catch(() => ({}));
      return stub.fetch(new Request(new URL(url.pathname, request.url), {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(body)
      }));
    }

    if (url.pathname === "/result" && request.method === "GET") {
      return stub.fetch(new Request(new URL(url.pathname + url.search, request.url)));
    }

    return json({
      service: "gungv-nexus-runtime",
      mode: env.NEXUS_MODE || "serverless",
      endpoints: ["/health", "/state", "/task", "/schedule", "/approve", "/run", "/result"],
      execution: "event-driven-autonomous",
      external_execution: false,
      arbitrary_code_execution: false
    });
  }
};

export class NexusState {
  constructor(state, env) {
    this.state = state;
    this.env = env;
  }

  async load() {
    return await this.state.storage.get("snapshot") || {
      status: "idle",
      worker: { wakeups: 0, last_wakeup_at: null, last_error: null },
      tasks: [],
      schedules: [],
      results: [],
      updated_at: nowIso()
    };
  }

  async save(snapshot) {
    snapshot.updated_at = nowIso();
    await this.state.storage.put("snapshot", snapshot);
  }

  async wakeSoon(delayMs = 1000) {
    await this.state.storage.setAlarm(Date.now() + Math.max(1, delayMs));
  }

  async fetch(request) {
    const url = new URL(request.url);
    const snapshot = await this.load();

    if (url.pathname === "/state") {
      return json({
        service: "gungv-nexus-runtime",
        persistent: true,
        execution: "event-driven-autonomous",
        external_execution: false,
        arbitrary_code_execution: false,
        ...snapshot
      });
    }

    if (url.pathname === "/task" && request.method === "POST") {
      const body = await request.json().catch(() => ({}));
      if (!body.task || typeof body.task !== "string") {
        return json({ error: "task must be a non-empty string" }, 400);
      }

      const item = {
        id: crypto.randomUUID(),
        task: body.task,
        action: typeof body.action === "string" ? body.action : "record",
        payload: body.payload ?? null,
        status: body.approval_required === false ? "queued" : "pending_approval",
        approval_required: body.approval_required !== false,
        created_at: nowIso(),
        attempts: 0
      };

      snapshot.tasks = [...snapshot.tasks.slice(-99), item];
      snapshot.status = item.status === "queued" ? "running" : "waiting_approval";
      await this.save(snapshot);
      if (item.status === "queued") await this.wakeSoon();
      return json({ accepted: true, task: item }, 202);
    }

    if (url.pathname === "/approve" && request.method === "POST") {
      const body = await request.json().catch(() => ({}));
      const item = snapshot.tasks.find(t => t.id === body.id);
      if (!item) return json({ error: "task_not_found" }, 404);
      if (item.status !== "pending_approval") return json({ error: "task_not_pending_approval", task: item }, 409);

      item.status = "queued";
      item.approved_at = nowIso();
      snapshot.status = "running";
      await this.save(snapshot);
      await this.wakeSoon();
      return json({ approved: true, task: item }, 202);
    }

    if (url.pathname === "/run" && request.method === "POST") {
      await this.wakeSoon(1);
      return json({ accepted: true, wakeup: "scheduled" }, 202);
    }

    if (url.pathname === "/schedule" && request.method === "POST") {
      const body = await request.json().catch(() => ({}));
      const at = Date.parse(body.at);
      if (!Number.isFinite(at)) return json({ error: "at must be an ISO-8601 date/time" }, 400);
      if (!body.task || typeof body.task !== "string") return json({ error: "task must be a non-empty string" }, 400);

      const item = {
        id: crypto.randomUUID(),
        task: body.task,
        action: typeof body.action === "string" ? body.action : "record",
        payload: body.payload ?? null,
        at: new Date(at).toISOString(),
        status: "scheduled",
        created_at: nowIso()
      };

      snapshot.schedules = [...snapshot.schedules.slice(-99), item];
      await this.save(snapshot);
      await this.scheduleNextAlarm(snapshot);
      return json({ accepted: true, schedule: item }, 202);
    }

    if (url.pathname === "/result" && request.method === "GET") {
      const id = url.searchParams.get("id");
      const result = snapshot.results.find(r => r.task_id === id);
      return result ? json(result) : json({ error: "result_not_found" }, 404);
    }

    return json({ error: "not_found" }, 404);
  }

  async executeTask(task) {
    const startedAt = nowIso();
    task.attempts = (task.attempts || 0) + 1;

    // Safe built-in actions only. No arbitrary JavaScript, shell, browser,
    // Android, credential, or destructive GitHub action is executed here.
    switch (task.action) {
      case "record":
        return {
          ok: true,
          action: "record",
          message: task.task,
          payload: task.payload ?? null
        };
      case "health_check":
        return {
          ok: true,
          action: "health_check",
          runtime: "gungv-nexus-runtime",
          persistent_state: true,
          autonomous_wakeup: true,
          external_execution: false
        };
      default:
        return {
          ok: false,
          action: task.action,
          error: "unsupported_action",
          allowed_actions: ["record", "health_check"]
        };
    }
  }

  async scheduleNextAlarm(snapshot) {
    const queued = snapshot.tasks.some(t => t.status === "queued");
    const pendingSchedules = snapshot.schedules
      .filter(s => s.status === "scheduled")
      .map(s => Date.parse(s.at))
      .filter(Number.isFinite);

    if (queued) {
      await this.wakeSoon(1000);
      return;
    }

    if (pendingSchedules.length) {
      const next = Math.min(...pendingSchedules);
      await this.state.storage.setAlarm(Math.max(Date.now() + 1, next));
      return;
    }

    await this.state.storage.deleteAlarm();
  }

  async alarm() {
    const snapshot = await this.load();
    snapshot.worker.wakeups += 1;
    snapshot.worker.last_wakeup_at = nowIso();
    snapshot.worker.last_error = null;

    try {
      const now = Date.now();

      // Promote due schedules into the task queue.
      for (const schedule of snapshot.schedules) {
        if (schedule.status === "scheduled" && Date.parse(schedule.at) <= now) {
          snapshot.tasks = [...snapshot.tasks.slice(-99), {
            id: schedule.id,
            task: schedule.task,
            action: schedule.action,
            payload: schedule.payload,
            status: "queued",
            approval_required: false,
            created_at: schedule.created_at,
            scheduled_at: schedule.at,
            attempts: 0
          }];
          schedule.status = "queued";
        }
      }

      const task = snapshot.tasks.find(t => t.status === "queued");
      if (task) {
        snapshot.status = "running";
        task.status = "running";
        task.started_at = nowIso();
        await this.save(snapshot);

        try {
          const output = await this.executeTask(task);
          task.status = output.ok ? "completed" : "failed";
          task.finished_at = nowIso();
          const result = {
            task_id: task.id,
            status: task.status,
            started_at: task.started_at,
            finished_at: task.finished_at,
            attempts: task.attempts,
            output
          };
          snapshot.results = [...snapshot.results.slice(-99), result];
        } catch (error) {
          task.status = "failed";
          task.finished_at = nowIso();
          snapshot.worker.last_error = String(error?.message || error);
          snapshot.results = [...snapshot.results.slice(-99), {
            task_id: task.id,
            status: "failed",
            started_at: task.started_at,
            finished_at: task.finished_at,
            attempts: task.attempts,
            output: { ok: false, error: snapshot.worker.last_error }
          }];
        }
      }

      snapshot.status = snapshot.tasks.some(t => t.status === "queued" || t.status === "running")
        ? "running"
        : snapshot.schedules.some(s => s.status === "scheduled")
          ? "scheduled"
          : "idle";

      await this.save(snapshot);
      await this.scheduleNextAlarm(snapshot);
    } catch (error) {
      snapshot.status = "error";
      snapshot.worker.last_error = String(error?.message || error);
      await this.save(snapshot);
      await this.wakeSoon(5000);
    }
  }
}
