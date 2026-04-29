import sys, nautical, json
args = sys.argv[1:]
open("log.txt", "w").write(json.dumps(args))
nautical.memory = json.loads(args[1].replace("'", "\""))
response = nautical.respond(args[0])
print(json.dumps(nautical.memory) + response)