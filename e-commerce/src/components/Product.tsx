import useProductStore from "../store/product.store";
import { useToast } from "../hooks/toast.hook";
import { Product as ProductType } from "../service/types";

export default function Product({ name, imgSrc, price, id }: ProductType) {
  const { addProductIntoCart } = useProductStore();
  const { triggerToast } = useToast();
  return (
    <div className="card w-96 shadow-xl h-72 bg-blue-950 bg-opacity-20 rounded-md">
      <figure className="h-40 min-h-40">
        <img height={400} src={imgSrc} />
      </figure>
      <div className="card-body">
        <h2 className="card-title flex items-center justify-between">
          <div>{name}</div>
          <div>
            <p>Ȼ {price}</p>
          </div>
        </h2>
        <button
          className="btn"
          onClick={() => {
            addProductIntoCart({ name, imgSrc, price, id, quantity: 1 });
            triggerToast(name + " added to cart");
          }}
        >
          Add to Cart
        </button>
      </div>
    </div>
  );
}
