import {
  createRequest,
  listRequests,
  removeRequest,
} from "../service/requestService";
import { Order } from "../service/types";
import useProductStore from "../store/product.store";

export const useRequest = () => {
  const { setOrders } = useProductStore();

  const updateOrders = async () => {
    const res = await listRequests();
    if (res) setOrders(res);
  };

  const removeOrder = async (request: Order) => {
    await removeRequest(request.request_id);
    updateOrders();
  };

  const createOrder = async (request: Order) => {
    await createRequest(request);
    updateOrders();
  };

  return { removeOrder, updateOrders, createOrder };
};
