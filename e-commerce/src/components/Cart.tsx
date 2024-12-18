import useProductStore from "../store/product.store";
import { useNavigate } from "react-router-dom";
import { useProduct } from "../hooks/product.hook";
import { Product } from "../service/types";

const Cart: React.FC = () => {
  const { productsAtCart, removeProductFromCart, handleQuantityChange } =
    useProductStore();
  const { calculateTotalPrice } = useProduct();
  const navigate = useNavigate();
  // const handleQuantityChange = (id: number, quantity: number) => {
  //   setCart((prevCart) =>
  //     prevCart.map((item) =>
  //       item.id === id ? { ...item, quantity: Math.max(1, quantity) } : item
  //     )
  //   );
  // };

  const handleRemoveItem = (product: Product) => {
    removeProductFromCart(product);
  };

  return (
    <div className="grid w-[600px] flex-grow mx-auto p-4">
      <div className="grid gap-4 flex-grow h-full items-start">
        {productsAtCart.map((product: Product) => (
          <div
            key={product.id}
            className="w-full bg-base-100 shadow-md p-4 flex justify-between items-center"
          >
            <div className="flex w-full items-center justify-between gap-2">
              <div className="grid">
                <h2 className="text-lg font-semibold">{product.name}</h2>
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="number"
                  min="1"
                  value={product.quantity}
                  onChange={(e) =>
                    handleQuantityChange(product, parseInt(e.target.value))
                  }
                  className="input input-bordered w-16 text-center"
                />
                <p className="w-24 justify-end flex text-lg text-secondary font-semibold">
                  ${product.price}
                </p>

                <button
                  onClick={() => handleRemoveItem(product)}
                  className="btn btn-error btn-sm"
                >
                  Remove
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-6">
        <h2 className="text-xl font-semibold">
          Total: ${calculateTotalPrice()}
        </h2>
        <button
          className="btn btn-primary mt-4"
          onClick={() => navigate("/checkout")}
        >
          Checkout
        </button>
      </div>
    </div>
  );
};

export default Cart;
