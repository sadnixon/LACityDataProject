import pandas as pd
import requests
import re

lot_parcel_area_regex = 'Lot/Parcel Area \(Calculated\)&nbsp;</a\\\\></td\\\\><td class=\\\\"DataCellsRight\\\\" \\\\>([0123456789,.]+) \(sq ft\)'

community_plan_area_regex = 'Community Plan Area&nbsp;</a\\\\></td\\\\><td class=\\\\"DataCellsRight\\\\" \\\\><a  href=\\\\"javascript:;\\\\" onclick=\\\\"ZimasData\.openDataLink\(\\\'COMN\\\', \\\'([^\\\\]+)\\\'\)'
area_planning_commission_regex = 'Area Planning Commission&nbsp;</a\\\\></td\\\\><td class=\\\\"DataCellsRight\\\\" \\\\><a  href=\\\\"javascript:;\\\\" onclick=\\\\"ZimasData\.openDataLink\(\\\'APC\\\', \\\'([^\\\\]+)\\\'\)'
neighborhood_council_regex = 'Neighborhood Council&nbsp;</a\\\\></td\\\\><td class=\\\\"DataCellsRight\\\\" \\\\><a  href=\\\\"javascript:;\\\\" onclick=\\\\"ZimasData\.openDataLink\(\\\'NC\\\', \\\'([^\\\\]+)\\\'\)'
council_district_regex = 'Council District&nbsp;</a\\\\></td\\\\><td class=\\\\"DataCellsRight\\\\" \\\\><a  href=\\\\"javascript:;\\\\" onclick=\\\\"ZimasData\.openDataLink\(\\\'COUNCIL\\\', \\\'([^\\\\]+)\\\'\)'

assessed_land_value_regex = 'Assessed Land Val\.&nbsp;</td\\\\><td class=\\\\"DataCellsRight\\\\" \\\\>\$([0123456789,]+)'
assessed_improvement_value_regex = 'Assessed Improvement Val\.&nbsp;</td\\\\><td class=\\\\"DataCellsRight\\\\" \\\\>\$([0123456789,.]+)'
last_owner_change_regex = 'Last Owner Change&nbsp;</td\\\\><td class=\\\\"DataCellsRight\\\\" \\\\>([0123456789/]+)'
last_sale_amount_regex = 'Last Sale Amount&nbsp;</td\\\\><td class=\\\\"DataCellsRight\\\\" \\\\>\$([0123456789,.]+)'

year_built_regex = (
    'Year Built&nbsp;</td\\\\><td class=\\\\"DataCellsRight\\\\" \\\\>(\d+)'
)
building_square_footage_regex = 'Building Square Footage&nbsp;</td\\\\><td class=\\\\"DataCellsRight\\\\" \\\\>([0123456789,.]+) \(sq ft\)'

df = pd.read_csv("Addresses_in_the_City_of_Los_Angeles.csv")

lot_parcel_areas = []
community_plan_areas = []
area_planning_commissions = []
neighborhood_councils = []
council_districts = []

assessed_land_values = []
assessed_improvement_values = []
last_owner_changes = []
last_sale_amounts = []

years_built = []
building_square_footages = []

for i, PIN in enumerate(df["PIN"]):
    r = requests.get("https://zimas.lacity.org/map.aspx?pin=" + PIN + "&ajax=yes")
    text_data = r.text

    lot_parcel_areas.append(
        float(re.search(lot_parcel_area_regex, text_data).group(1).replace(",", ""))
    )
    try:
        community_plan_areas.append(
            re.search(community_plan_area_regex, text_data).group(1)
        )
    except:
        community_plan_areas.append("None")
    try:
        area_planning_commissions.append(
            re.search(area_planning_commission_regex, text_data).group(1)
        )
    except:
        area_planning_commissions.append("None")
    try:
        neighborhood_councils.append(
            re.search(neighborhood_council_regex, text_data).group(1)
        )
    except:
        neighborhood_councils.append("None")
    try:
        council_districts.append(re.search(council_district_regex, text_data).group(1))
    except:
        council_districts.append("None")
    try:
        assessed_land_values.append(
            float(
                re.search(assessed_land_value_regex, text_data)
                .group(1)
                .replace(",", "")
            )
        )
    except:
        assessed_land_values.append("None")
    try:
        assessed_improvement_values.append(
            float(
                re.search(assessed_improvement_value_regex, text_data)
                .group(1)
                .replace(",", "")
            )
        )
    except:
        assessed_improvement_values.append("None")
    try:
        last_owner_changes.append(
            re.search(last_owner_change_regex, text_data).group(1)
        )
    except:
        last_owner_changes.append("None")
    try:
        last_sale_amounts.append(
            float(
                re.search(last_sale_amount_regex, text_data).group(1).replace(",", "")
            )
        )
    except:
        last_sale_amounts.append("None")

    year_built_list = list(
        filter(lambda x: x != "0", re.findall(year_built_regex, text_data))
    )
    building_square_footage_list = list(
        filter(lambda x: x != "0", re.findall(building_square_footage_regex, text_data))
    )

    if year_built_list == []:
        years_built.append("None")
    else:
        years_built.append(min([int(x) for x in year_built_list]))
    if building_square_footage_list == []:
        building_square_footages.append("None")
    else:
        building_square_footages.append(
            sum([float(x.replace(",", "")) for x in building_square_footage_list])
        )

    if i % 10000 == 0:
        print(i)
        compiled_list = [
            lot_parcel_areas,
            community_plan_areas,
            area_planning_commissions,
            neighborhood_councils,
            council_districts,
            assessed_land_values,
            assessed_improvement_values,
            last_owner_changes,
            last_sale_amounts,
            years_built,
            building_square_footages,
        ]
        so_far = pd.DataFrame(compiled_list)
        so_far.to_csv("so_far.csv")

df["lot_parcel_area"] = lot_parcel_areas
df["community_plan_area"] = community_plan_areas
df["area_planning_commission"] = area_planning_commissions
df["neighborhood_council"] = neighborhood_councils
df["council_district"] = council_districts

df["assessed_land_value"] = assessed_land_values
df["assessed_improvement_values"] = assessed_improvement_values
df["last_owner_change"] = last_owner_changes
df["last_sale_amount"] = last_sale_amounts

df["year_built"] = years_built
df["building_square_footage"] = building_square_footages

df.to_csv("final_la_address_data.csv")
