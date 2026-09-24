#!/usr/bin/env python3
import argparse, json
from kernel.runtime import NexusRuntime

p=argparse.ArgumentParser(prog="nexus")
sub=p.add_subparsers(dest="command",required=True)
h=sub.add_parser("health")
t=sub.add_parser("route"); t.add_argument("task")
a=sub.add_parser("inspect"); a.add_argument("operation"); a.add_argument("--source",default="internal")
args=p.parse_args(); n=NexusRuntime(".")
if args.command=="health": print(json.dumps(n.health(),indent=2))
elif args.command=="route": print(json.dumps(n.handle(args.task),indent=2,ensure_ascii=False))
elif args.command=="inspect": print(json.dumps(n.security.inspect(args.operation,args.source),indent=2))
