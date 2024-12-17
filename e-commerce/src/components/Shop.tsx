import Product from "./Product";
import shokunin from "../assets/shokunin.jpg";
import merc from "../assets/merc.jpg";
import octane from "../assets/octane.jpg";
import fennec from "../assets/fennec.jpg";

export default function Shop() {
  return (
    <div className="flex w-full p-12 gap-2 overflow-auto">
      <Product
      id="fennec"
        title="Fennec"
        imgSrc={fennec}
        price="800"
      />
      <Product
        id="shokunin"
        title="Shokunin"
        imgSrc={shokunin}
        price="1000"
      />
      <Product
        id="octane"
        title="Octane"
        imgSrc={octane}
        price="10"
      />
      <Product
        id="merc"
        title="Merc"
        imgSrc={merc}
        price="300"
      />
    </div>
  );
}
