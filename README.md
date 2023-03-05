# ANTI-HURRICANE-HURRICANE-CLUB
Building a Dashboard to visualize Social Vulnerability Indices (SVI) in Puerto Rico.

##  Impact of the project on Social Threats
Different communities are unequal in terms of their SVIs. Some factors can be used as proxy to estimate which communities are not as strongly prepared in the event of natural disasters, like hurricanes. The dashboard we've created helps to visualize the range in these Indices amongst county, and identify which are more at risk than others. 

As described by the ATSDR:
> SVI can be used to:
> - Allocate emergency preparedness funding by community need.
> - Estimate the amount and type of needed supplies like food, water, medicine, and bedding.
> - Decide how many emergency personnel are required to assist people.
> - Identify areas in need of emergency shelters.
> - Create a plan to evacuate people, accounting for those who have special needs, such as those without vehicles, the elderly, or people who do not understand English well.
> - Identify communities that will need continued support to recover following an emergency or naturals disaster.

## Information about Dataset
[This dataset](https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html) was created by ATSDR’s Geospatial Research, Analysis & Services Program (GRASP).

It contains ‘Social Vulnerability Indices’ per subdivision of counties area of Puerto Rico for the years 2016 and 2018.  The 15 variables are categorized into four themes: Socioeconomic Status, Household Composition & Disability, Minority Status & Language, and Housing Type & Transportation. 

The dataset contains over 120 columns because it contains many estimates per variable [count (E_)+ MOE (M_), percentage (EP_)+ MOE (MP_), percentile (EPL_),  percentile ranking, flags for percentage >90th percentile (F_)], values aggregated per theme (sum (SPL_) + percentile ranking (RPL_), flags (F_). 

### Variable descriptions
- _TOTPOP: Population
- _HU: Housing units
- _HH: Households
- _POV:  Persons below poverty
- _UNEMP: Civilian (age 16+) unemployed
- _PCI: Per capita income
- _NOHSDP: Persons (age 25+) with no high school diploma
- _AGE65: Persons aged 65 and older
- _AGE17: Persons aged 17 and younger
- _DISABL: Civilian noninstitutionalized population with a disability
- _SNGPNT: Single parent household with children under 18
- _MINRTY: Minority (all persons except white, non-Hispanic
- _LIMENG: Persons (age 5+) who speak English "less than well"
- _MUNIT: Housing in structures with 10 or more units
- _MOBILE: Mobile homes
- _CROWD: At household level (occupied housing units), more people than rooms
- _NOVEH: Households with no vehicle available
- _GROUPQ: Persons in institutionalized and noninstitutionalized group quarters


## Dashboard Features
First off, a user may choose which year is applied to the graphs, between 2016 and 2018. They could track thus the difference SVI's in counties before and after Hurricane Maria (2017). As well, a user may filter by county population.

This Dashboard contains three graphs (so far). The first is a sorted bar plot of counties, showing the count of a variable the user's chose via a dropdown. The user is able to scroll down and see the values for everycounty. A tooltip is applied to the user can see exactly the value of the variable. This allows the user to see which county has, for example, the greatest population. 

The second graph is a scatterplot where a user may choose two variables to compare. The user could analyze the trend, and see if some are correlated with each other. 

The final plot allows the user to select specific counties to compare in a barchart with a specific variable. This helps the user to visualize a narrowed down list of counties, to compare those of interest with more ease.


### References
[CDC/ATSDR SVI Fact Sheet](https://www.atsdr.cdc.gov/placeandhealth/svi/fact_sheet/fact_sheet.html)
[Dataset](https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html)
