export default {
  async fetch(request, env) {
    if (request.method !== "POST") {
      return new Response("Send a POST request with JSON data.");
    }  

    const data = await request.json()
    const { user_input } = data;
    console.log(data)
    
    // messages - chat style input
    let chat = {
      messages: [
        { role: 'system', content: 'Help me with me Japanese Language Learning' },
        { role: 'user', content: user_input }
      ]
    };
    const response = await env.AI.run('@cf/meta/llama-3-8b-instruct', chat);
    return Response.json(response);
  }
};