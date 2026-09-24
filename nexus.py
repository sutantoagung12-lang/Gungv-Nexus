#!/usr/bin/env python3
import argparse
import json
from kernel.runtime import NexusRuntime

def main():
    p=argparse.ArgumentParser(prog="nexus")
    sub=p.add_subparsers(dest="command", required=True)
    sub.add_parser("health")
    t=sub.add_parser("route"); t.add_argument("task")
    i=sub.add_parser("inspect"); i.add_argument("operation"); i.add_argument("--source",default="internal")
    r=sub.add_parser("remember"); r.add_argument("content"); r.add_argument("--type",default="observation")
    args=p.parse_args()
    n=NexusRuntime(".")
    if args.command=="health":
        out=n.health()
    elif args.command=="route":
        out=n.handle(args.task)
    elif args.command=="inspect":
        out=n.security.inspect(args.operation,args.source)
    else:
        out=n.memory.add({"content":args.content,"type":args.type})
    print(json.dumps(out, indent=2, ensure_ascii=False, default=str))

if __name__=="__main__":
    main()
