import Product from "./Product";

export default function Shop() {
  return (
    <div className="flex w-full p-12 gap-2 overflow-auto">
      <Product
        title="Fennec"
        imgSrc="https://api3.win.gg/wp-content/uploads/2022/03/maxresdefault-31.jpg"
        price="800"
      />
      <Product
        title="Shokunin"
        imgSrc="https://itempreviews.rocket-league.com/78fcada939d9d717c3d24898f9abed50de36d2951622177f3a2cafcbc800baa0.jpg"
        price="1000"
      />
      <Product
        title="Octane"
        imgSrc="https://www.rlcd.gg/wp-content/uploads/2017/12/Rocket-League-Octane-Car-Stats.jpg"
        price="10"
      />
      <Product
        title="Merc"
        imgSrc="https://mrwallpaper.com/images/high/colorful-merc-rocket-league-car-2k-6s0orakodz1t0q7x.jpg"
        price="300"
      />
    </div>
  );
}
