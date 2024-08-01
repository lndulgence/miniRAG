package main

import "os"

type Args struct {
	llamaurl  string
	llamaport string
	ragurl    string
	ragport   string
	sysprompt string
}

func getArgs() Args {
	llamaurl, ok := os.LookupEnv("LLAMA_HTTP_HOST")

	if !ok {
		llamaurl = "local-llama.default.svc.cluster.local"
	}
	llamaport, ok := os.LookupEnv("LLAMA_HTTP_PORT")
	if !ok {
		llamaport = "8000"
	}
	ragurl, ok := os.LookupEnv("RAG_HTTP_HOST")
	if !ok {
		ragurl = "ragapi.default.svc.cluster.local"
	}
	ragport, ok := os.LookupEnv("RAG_HTTP_PORT")
	if !ok {
		ragport = "8000"
	}
	sysprompt, ok := os.LookupEnv("SYSPROMPT")
	if !ok {
		sysprompt = "You are a friendly AI assistant. Your language is diligent, and your purpose is to help. Your attitude is friendly, and your tone is formal."
	}
	return Args{llamaurl, llamaport, ragurl, ragport, sysprompt}
}
