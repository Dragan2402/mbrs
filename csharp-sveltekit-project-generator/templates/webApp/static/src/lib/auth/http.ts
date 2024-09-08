import { env } from '../../env';
import type { ApiConfig, RequestParams } from '$lib/api/apiV1';
import { Api as ApiV1 } from '$lib/api/apiV1';

async function getRequestHeaders(): Promise<HeadersInit> {
  // Place to add JWT
  return {};
}

const apiConfig: ApiConfig = {
  baseUrl: env.baseUrl,
  baseApiParams: {
    secure: true
  },
  securityWorker: async (): Promise<RequestParams> => {
    const requestParams: RequestParams = {};
    requestParams.headers = await getRequestHeaders();
    return requestParams;
  }
};

const api = {
  v1: new ApiV1(apiConfig)
};

export default api;
