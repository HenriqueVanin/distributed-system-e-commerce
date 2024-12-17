import useProductStore from "../store/product.store";

export const useProduct = () => {
  const { productsAtCart } = useProductStore();
  const calculateTotalQuantity = (): number => {
    return productsAtCart
      .map((item) => Number(item.quantity)) // Converte 'price' para string e depois para número
      .reduce((sum, quantity) => sum + quantity, 0); // Soma os valores
  };
  const calculateTotalPrice = (): number => {
    return productsAtCart
      .map((item) => Number(item.price) * item.quantity) // Converte 'price' para string e depois para número
      .reduce((sum, price) => sum + price, 0); // Soma os valores
  };

  return {
    calculateTotalQuantity,
    calculateTotalPrice,
  };
};
