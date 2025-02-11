import useProductStore from "../store/product.store";
import { useNavigate } from "react-router-dom";
import { useProduct } from "../hooks/product.hook";
import { Product } from "../service/types";
import { createRequest } from "../service/requestService";

const Cart: React.FC = () => {
  const { productsAtCart } = useProductStore();

  const { storageProducts } = useProductStore();
  const { calculateTotalPrice, removeProductFromCart, updateProductAtCart } =
    useProduct();
  const navigate = useNavigate();

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
                  onChange={(e) => {
                    const storageQuantity =
                      storageProducts.find((p) => p.id === product.id)
                        ?.quantity ?? 0;
                    updateProductAtCart({
                      ...product,
                      quantity:
                        storageQuantity >= parseInt(e.target.value)
                          ? parseInt(e.target.value)
                          : storageQuantity,
                    });
                  }}
                  className="input input-bordered w-16 text-center"
                />
                <p className="w-24 justify-end flex text-lg text-secondary font-semibold">
                  ${product.price}
                </p>

                <button
                  onClick={() => removeProductFromCart(product)}
                  className="btn btn-error btn-sm"
                >
                  Remove
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
      {productsAtCart.length !== 0 ? (
        <div className="mt-6 flex items-center justify-between">
          <h2 className="text-xl font-semibold">
            Total: ${calculateTotalPrice()}
          </h2>
          <button
            className="btn btn-primary items-center"
            onClick={() => {
              navigate("/checkout");
              createRequest({
                total: calculateTotalPrice().toString(),
                client_id: "1",
              });
            }}
          >
            Checkout
          </button>
        </div>
      ) : (
        <div className="mt-6">
          <h2 className="text-xl font-semibold">Cart is empty</h2>
        </div>
      )}
    </div>
  );
};

export default Cart;
