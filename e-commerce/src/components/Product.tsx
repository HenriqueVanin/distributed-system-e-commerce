import useProductStore, { ProductProps } from "../store/product.store";

export default function Product({ title, imgSrc, price, id }: ProductProps) {
  const {addProductIntoCart} = useProductStore()
  return (
    <div className="card w-96 shadow-xl h-72 bg-blue-950 bg-opacity-20">
      <figure className="h-40 min-h-40">
        <img
          height={400}
          src={imgSrc}
        />
      </figure>
      <div className="card-body">
        <h2 className="card-title flex items-center justify-between">
          <div>{title}</div>
          <div>
            <p>Ȼ {price}</p>
          </div>
        </h2>
        <button className="btn" onClick={() => addProductIntoCart({title, imgSrc, price, id})}>Add to Cart</button>
      </div>
    </div>
  );
}
