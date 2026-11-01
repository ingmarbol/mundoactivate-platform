import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 1,
  iterations: 5,
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<400'],
  },
};

export default function () {
  // Set BASE_URL only to an authorized non-production endpoint.
  const baseUrl = __ENV.BASE_URL || 'http://127.0.0.1:8080';
  const response = http.get(`${baseUrl}/health`);
  check(response, { 'health returns 200': (r) => r.status === 200 });
}

