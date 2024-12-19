import useProductStore from "../store/product.store";
// import { useProduct } from "../hooks/product.hook";
import { Order } from "../service/types";
import { useEffect } from "react";
import { useRequest } from "../hooks/request.hook";

const Orders: React.FC = () => {
  const { updateOrders } = useRequest();
  const { orders } = useProductStore();
  useEffect(() => {
    updateOrders();
  }, []);

  return (
    <div className="grid w-[600px] flex-grow mx-auto p-4">
      <div className="grid gap-4 flex-grow h-full items-start">
        {orders.map((order: Order) => (
          <div
            key={order.request_id}
            className="w-full bg-base-100 shadow-md p-4 flex justify-between items-center"
          >
            <div className="flex w-full items-center justify-between gap-2">
              <div className="grid">
                <h2 className="text-lg font-semibold">{order.status}</h2>
              </div>
              <div className="flex items-center gap-2">
                <p className="w-24 justify-end flex text-lg text-secondary font-semibold">
                  ${order.total}
                </p>

                {/* <button
                  onClick={() => removeProductFromCart(order)}
                  className="btn btn-error btn-sm"
                >
                  Remove
                </button> */}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Orders;
