const json = (data, status = 200) => new Response(JSON.stringify(data, null, 2), {
  status,
  headers: { "content-type": "application/json; charset=utf-8" }
});

function stateId(env, key = "default") {
  return env.NEXUS_STATE.idFromName(key);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const key = url.searchParams.get("key") || "default";
    const stub = env.NEXUS_STATE.get(stateId(env, key));

    if (url.pathname === "/health") return stub.fetch(new Request(new URL("/state", request.url)));
    if (url.pathname === "/state") return stub.fetch(new Request(new URL("/state", request.url)));

    if ((url.pathname === "/task" || url.pathname === "/schedule") && request.method === "POST") {
      const body = await request.json().catch(() => ({}));
      return stub.fetch(new Request(new URL(url.pathname, request.url), {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(body)
      }));
    }

    return json({
      service: "gungv-nexus-runtime",
      mode: env.NEXUS_MODE || "serverless",
      endpoints: ["/health", "/task", "/schedule", "/state"],
      execution: "event-driven",
      external_execution: false
    });
  }
};

export class NexusState {
  constructor(state, env) {
    this.state = state;
    this.env = env;
  }

  async fetch(request) {
    const url = new URL(request.url);
    let snapshot = await this.state.storage.get("snapshot") || {
      status: "idle", tasks: [], schedules: []
    };

    if (url.pathname === "/state") {
      return json({
        service: "gungv-nexus-runtime",
        persistent: true,
        execution: "event-driven",
        external_execution: false,
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
        status: "queued",
        approval_required: body.approval_required !== false,
        created_at: new Date().toISOString()
      };
      snapshot.tasks = [...snapshot.tasks.slice(-99), item];
      snapshot.updated_at = new Date().toISOString();
      await this.state.storage.put("snapshot", snapshot);
      return json({ accepted: true, task: item }, 202);
    }

    if (url.pathname === "/schedule" && request.method === "POST") {
      const body = await request.json().catch(() => ({}));
      if (!body.at) return json({ error: "at is required" }, 400);
      const item = {
        id: crypto.randomUUID(),
        task: body.task || "scheduled Nexus task",
        at: body.at,
        status: "scheduled",
        created_at: new Date().toISOString()
      };
      snapshot.schedules = [...snapshot.schedules.slice(-99), item];
      snapshot.updated_at = new Date().toISOString();
      await this.state.storage.put("snapshot", snapshot);
      return json({ accepted: true, schedule: item }, 202);
    }

    return json({ error: "not_found" }, 404);
  }
}
