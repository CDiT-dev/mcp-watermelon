const BASE_URL = "https://public.watermelon.ai";

export interface WatermelonClientConfig {
  apiKey: string;
  secretKey: string;
}

export class WatermelonClient {
  private token: string;

  constructor(config: WatermelonClientConfig) {
    this.token = `${config.apiKey}.${config.secretKey}`;
  }

  async request<T = unknown>(
    method: string,
    path: string,
    body?: unknown,
  ): Promise<T> {
    const url = `${BASE_URL}${path}`;
    const headers: Record<string, string> = {
      Authorization: `Bearer ${this.token}`,
      "Content-Type": "application/json",
    };

    const res = await fetch(url, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!res.ok) {
      const text = await res.text().catch(() => "");
      if (res.status === 429) {
        throw new Error(`Rate limit exceeded (429). ${text}`);
      }
      throw new Error(`Watermelon API error ${res.status}: ${text}`);
    }

    if (res.status === 204) {
      return undefined as T;
    }

    return res.json() as Promise<T>;
  }

  get(path: string) {
    return this.request("GET", path);
  }

  post(path: string, body: unknown) {
    return this.request("POST", path, body);
  }

  put(path: string, body: unknown) {
    return this.request("PUT", path, body);
  }

  del(path: string) {
    return this.request("DELETE", path);
  }
}
