import fetch from 'node-fetch';

export interface AnthropicOptions {
  model?: string;
  max_tokens?: number;
}

export async function anthropicComplete(prompt: string, options: AnthropicOptions = {}): Promise<string> {
	const apiKey = process.env.ANTHROPIC_API_KEY;
	if (!apiKey) throw new Error('Missing ANTHROPIC_API_KEY');
	const url = 'https://api.anthropic.com/v1/messages';
	const res = await fetch(url, {
		method: 'POST',
		headers: {
			'content-type': 'application/json',
			'x-api-key': apiKey,
			'anthropic-version': '2023-06-01'
		},
		body: JSON.stringify({
			model: options.model || 'claude-3-5-sonnet-latest',
			max_tokens: options.max_tokens || 1024,
			messages: [
				{ role: 'user', content: prompt }
			]
		})
	});
	if (!res.ok) throw new Error(`Anthropic error ${res.status}: ${await res.text()}`);
	const data: any = await res.json();
	const text = data?.content?.[0]?.text ?? '';
	return text;
}
