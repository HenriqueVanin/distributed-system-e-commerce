import api from './api'; // Importa a instância do Axios
import { Request } from './types'; // Importa os tipos

// Listar pedidos
export const listRequests = async (): Promise<Request[]> => {
  const response = await api.get<Request[]>('/requests');
  return response.data;
};

// Criar pedido
export const createRequest = async (request: Omit<Request, 'request_id' | 'total' | 'status'>): Promise<Request> => {
  const response = await api.post<Request>('/requests', request);
  return response.data;
};

// Remover pedido
export const removeRequest = async (requestId: string): Promise<void> => {
  await api.delete(`/requests/${requestId}`);
};
