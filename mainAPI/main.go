package main

import (
	"mainAPI/prompts"
	"mainAPI/rest"
)

func main() {
	// Get the arguments
	args := getArgs()

	// Create the full URLs for the RAG and Llama services
	fullRagURL := "http://" + args.ragurl + ":" + args.ragport + "/augment"
	fullLlamaURL := "http://" + args.llamaurl + ":" + args.llamaport + "/chat"

	// Create a new prompter
	prompter := prompts.NewPrompter(args.sysprompt, fullRagURL, fullLlamaURL)

	// Start the REST API
	startRestAPI(prompter)

}

func startRestAPI(p *prompts.Prompter) {
	// Start the REST API
	r := rest.NewRouter(p)
	r.Run(":8080")
}
