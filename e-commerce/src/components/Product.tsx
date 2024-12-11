interface ProductProps {
  title: string;
  imgSrc: string;
  price: string;
}

export default function Product({ title, imgSrc, price }: ProductProps) {
  return (
    <div className="card w-96 shadow-xl bg-blue-950">
      <figure>
        <img
          height={500}
          src={imgSrc}
          alt="Shoes"
          className="overflow-hidden"
        />
      </figure>
      <div className="card-body">
        <h2 className="card-title flex items-center justify-between">
          <div>{title}</div>
          <div>
            <p>Ȼ {price}</p>
          </div>
        </h2>
        <button className="btn">Buy</button>
      </div>
    </div>
  );
}
