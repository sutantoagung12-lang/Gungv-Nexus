# Nexus Tool & Skill Matrix

Gungv-Nexus now has a repository-level inventory describing how available tool and skill classes map onto the Nexus lifecycle.

The registry is descriptive, not a claim that every provider is installed, authenticated, reachable, or production-ready. Runtime detection remains authoritative.

## Lifecycle mapping

DISCOVER -> GitHub + Exa + Firecrawl + Tavily  
RETRIEVE -> Basic Memory + Cortex + Engram  
PLAN -> Agent RouteKit  
EXECUTE -> TinyFish + Remote Desktop Commander + Floot  
CHECKPOINT/PERSIST -> Supabase + Basic Memory  
SCHEDULE -> Automations  
DEPLOY -> Vercel + Railway + Render  
VERIFY -> Qodo/CodeRabbit + AgentProof  
LEARN -> Memory systems  
EVOLVE -> Route selection + evidence + Nexus governance

## Safety boundary

Nexus does not copy external tool implementations into the core merely because a tool exists. Adapters must observe runtime availability, keep credentials outside source control, validate external data, and preserve confirmation gates for destructive operations.

## Android constraint

Browser/device execution remains endpoint-dependent. Android Chrome CDP is a Nexus adapter boundary; availability of a ChatGPT connector does not imply that the user's Android device is reachable.

## Next integration layer

The registry is intended to feed capability discovery and routing. A future runtime adapter can translate observed connector availability into Nexus capability nodes without treating configuration as proof of reachability.
