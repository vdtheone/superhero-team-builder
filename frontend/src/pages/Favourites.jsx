import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

function Favourites() {
  const [favourites, setFavourites] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/favourites/")
      .then((res) => {
        setFavourites(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const removeFavourite = (favId) => {
    api.delete(`/favourites/${favId}/delete/`)
      .then(() => {
        setFavourites((prev) => prev.filter((fav) => fav.id !== favId));
      })
      .catch((err) => console.error(err));
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">
        Favourite Superheroes
      </h1>
      
      {favourites.length === 0 ? (
        <p>You haven't added any favourites yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {favourites.map((fav) => (
            <div key={fav.id} className="bg-white shadow rounded p-4 flex flex-col justify-between">
              <div className="flex flex-col gap-4">
                {fav.superhero_details?.image_url && (
                  <img
                    src={fav.superhero_details.image_url}
                    alt={fav.superhero_details.name}
                    referrerPolicy="no-referrer"
                    className="w-full h-48 rounded object-cover bg-gray-200"
                  />
                )}
                <div>
                  <Link to={`/hero/${fav.superhero}`} className="text-xl font-bold hover:underline">
                    {fav.superhero_details?.name || fav.hero_name}
                  </Link>
                  <div className="mt-1 text-sm text-gray-600">
                    <p>Intelligence: {fav.superhero_details?.intelligence}</p>
                    <p>Strength: {fav.superhero_details?.strength}</p>
                  </div>
                </div>
              </div>
              <button
                onClick={() => removeFavourite(fav.id)}
                className="mt-4 text-red-600 hover:text-red-800 text-sm font-semibold self-start"
              >
                Remove from Favourites
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Favourites;