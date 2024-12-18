import { create } from "zustand";
import { Product } from "../service/types";

// Definindo a interface do estado e das ações
interface ProductState {
  storageProducts: Product[];
  setStorageProducts: (p: Product[]) => void;
  productsAtCart: Product[];
  setProductsAtCart: (p: Product[]) => void;
  addProductIntoCart: (product: Product) => void;
  clearCart: () => void;
  removeProductFromCart: (product: Product) => void;
  handleQuantityChange: (product: Product, newQuantity: number) => void;
}

// Criando o store com tipos em TypeScript
const useProductStore = create<ProductState>((set) => ({
  productsAtCart: [],
  setProductsAtCart: (p: Product[]) => set({ productsAtCart: p }),
  storageProducts: [],
  setStorageProducts: (p: Product[]) => set({ storageProducts: p }),
  clearCart: () => set({ productsAtCart: [] }),
  addProductIntoCart: (product: Product) =>
    set((state) => ({
      productsAtCart: state.productsAtCart
        .map((p) =>
          p.id === product.id ? { ...p, quantity: p.quantity + 1 } : p
        )
        .concat(
          state.productsAtCart.some((p) => p.id === product.id)
            ? []
            : { ...product, quantity: 1 }
        ),
    })),

  removeProductFromCart: (product: Product) =>
    set((state) => ({
      productsAtCart: state.productsAtCart.filter(
        (item) => item.id !== product.id
      ), // Remove o item específico
    })),
  handleQuantityChange: (product: Product, newQuantity: number) =>
    set((state) => ({
      productsAtCart: state.productsAtCart.map((p) =>
        p.id === product.id ? { ...p, quantity: newQuantity } : p
      ),
    })),
}));

export default useProductStore;
