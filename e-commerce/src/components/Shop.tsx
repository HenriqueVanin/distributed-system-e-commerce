import Product from "./Product";
import { useEffect } from "react";
import useProductStore from "../store/product.store";
import { useProduct } from "../hooks/product.hook";

export default function Shop() {
  const { storageProducts } = useProductStore();
  const { updateShop, getCart } = useProduct();

  useEffect(() => {
    updateShop();
    getCart();
  }, []);

  return (
    <div className="flex w-full p-24 gap-4 overflow-auto">
      {storageProducts?.map((product) => (
        <Product
          id={product?.id}
          name={product?.name}
          imgSrc={"/" + product?.imgSrc}
          price={product?.price}
          quantity={product?.quantity}
        />
      ))}
    </div>
  );
}
