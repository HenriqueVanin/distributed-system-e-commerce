import api from "./api"; // Importa a instância do Axios
import { Order, RequestPayload } from "./types"; // Importa os tipos

// Listar pedidos
export const listRequests = async (): Promise<Order[]> => {
  const response = await api.get<Order[]>("/requests");
  return response.data;
};

// Criar pedido
export const createRequest = async (request: RequestPayload) => {
  await api.post<RequestPayload>("/requests", request);
};

// Remover pedido
export const removeRequest = async (requestId: string): Promise<void> => {
  await api.delete(`/requests/${requestId}`);
};
