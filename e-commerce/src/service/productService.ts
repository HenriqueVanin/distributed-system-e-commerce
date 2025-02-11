import api from "./api"; // Importa a instância do Axios
import { Product } from "./types"; // Importa os tipos

// Listar produtos
export const listProducts = async (): Promise<Product[]> => {
  const response = await api.get<Product[]>("/principal/products");
  return response.data;
};

// Criar produto
export const createProduct = async (product: Product): Promise<Product> => {
  const response = await api.post<Product>("/principal/products", product);
  return response.data;
};

// Atualizar produto
export const updateProduct = async (
  productId: string,
  product: Partial<Omit<Product, "id">>
): Promise<Product> => {
  const response = await api.put<Product>(
    `/principal/products/${productId}`,
    product
  );
  return response.data;
};

// Remover produto
export const removeProduct = async (productId: string): Promise<void> => {
  await api.delete(`/principal/products/${productId}`);
};

export const clearCart = async (): Promise<void> => {
  await api.post("/principal/clear_products");
};

export const fetchStock = async (): Promise<Product[]> => {
  const response = await api.get<Product[]>("/principal/check_storage");
  return response.data; // Retorna apenas a lista de itens do estoque
};
