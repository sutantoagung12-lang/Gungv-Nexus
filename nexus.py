#!/usr/bin/env python3
import argparse
import json
from kernel.runtime import NexusRuntime
from cognition.orchestration import OrchestrationCycle

def main():
    p=argparse.ArgumentParser(prog="nexus")
    sub=p.add_subparsers(dest="command", required=True)
    sub.add_parser("health")
    sub.add_parser("colibri-health")
    t=sub.add_parser("route"); t.add_argument("task")
    i=sub.add_parser("inspect"); i.add_argument("operation"); i.add_argument("--source",default="internal")
    r=sub.add_parser("remember"); r.add_argument("content"); r.add_argument("--type",default="observation")
    c=sub.add_parser("cycle"); c.add_argument("goal"); c.add_argument("task")
    cc=sub.add_parser("colibri-chat"); cc.add_argument("message")
    args=p.parse_args()
    n=NexusRuntime(".")
    if args.command=="health":
        out=n.health()
    elif args.command=="colibri-health":
        out=n.colibri_status()
    elif args.command=="route":
        out=n.handle(args.task)
    elif args.command=="inspect":
        out=n.security.inspect(args.operation,args.source)
    elif args.command=="cycle":
        out=n.run_cycle(args.goal,args.task)
    elif args.command=="colibri-chat":
        out=n.colibri_chat([{"role":"user","content":args.message}])
    else:
        out=n.memory.add({"content":args.content,"type":args.type})
    print(json.dumps(out, indent=2, ensure_ascii=False, default=str))

if __name__=="__main__":
    main()
