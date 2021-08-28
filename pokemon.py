import requests
import json


class Pokemonhunter:
    def parse_configurations(self, parameter):
        with open("projectconfig.json", "r") as jsonobj:
            jsonresponse = json.load(jsonobj)
            if jsonresponse.get(parameter) is not None:
                return jsonresponse.get(parameter)
            else:
                raise Exception("Unable to parse json configuration for %s" % parameter)

    def get_pokemons(self, url):
        querystring = {
            "limit": self.parse_configurations("limit"),
            "offset": self.parse_configurations("offset")
        }

        response = requests.request(
            "GET",
            url,
            params=querystring
        )

        if response.status_code == 200:
            return response.json()

        else:
            raise Exception("Status code is %d" % response.status_code)

    def get_pokemon_details(self):
        pokemon_overview = self.get_pokemons(self.parse_configurations("endpoint"))
        if pokemon_overview.get("results") is not None:
            for item in (pokemon_overview.get("results")):
                name = item.get("name")
                print(name)
                response = self.get_pokemons(item.get("url"))
                if len(response.get("abilities")) < 2:
                    single_ability = {
                        "ability": {"name": response.get("abilities")[0].get("ability").get("name"),
                                    "url": response.get("abilities")[0].get("ability").get("url")
                                    }
                    }
                    print(single_ability)
                if len(response.get("abilities")) >= 2:
                    multiple_ability = response.get("abilities")
                    new_list = [{k: v for k, v in d.items() if k != 'is_hidden' and k != 'slot'} for d in
                                multiple_ability]
                    print(new_list)

                # for ability in response.get("abilities"):
                #     if len(response.get("abilities")) < 2:
                #         ability = ability.get("ability").get("name")
                #     else:
                #         [item for item inability.get("ability").get("name")
                #     print(ability)


p = Pokemonhunter()
p.get_pokemon_details()