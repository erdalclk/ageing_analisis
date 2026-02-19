import pandas as pd
import numpy as np


def load_data(pop_path, life_path):
    pop = pd.read_csv(pop_path)
    life = pd.read_csv(life_path)

    pop = pop[["Location","Time","Sex","Age","Value"]]
    life = life[["Location","Time","Sex","Age","Value"]]

    for df in [pop, life]:
        df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
        df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

    pop = pop[(pop["Time"]==2018) & (pop["Sex"]=="Both sexes")]
    life = life[(life["Time"]==2018) & (life["Sex"]=="Both sexes")]

    pop.columns = ["Country","Year","Sex","Age","Population"]
    life.columns = ["Country","Year","Sex","Age","ex"]

    df = pd.merge(pop, life, on=["Country","Year","Sex","Age"])
    return df


def calculate_indicators(df):
    results = []

    for country in df["Country"].unique():
        d = df[df["Country"]==country]

        total = d["Population"].sum()
        pop_0_14 = d[(d["Age"]>=0)&(d["Age"]<=14)]["Population"].sum()
        pop_15_64 = d[(d["Age"]>=15)&(d["Age"]<=64)]["Population"].sum()
        pop_65 = d[d["Age"]>=65]["Population"].sum()
        pop_20_68 = d[(d["Age"]>=20)&(d["Age"]<=68)]["Population"].sum()
        pop_69 = d[d["Age"]>=69]["Population"].sum()

        prop65 = pop_65/total*100
        oadr = pop_65/pop_15_64*100
        ai = pop_65/pop_0_14*100
        aa = (d["Age"]*d["Population"]).sum()/total
        prop_rle15 = pop_69/total*100
        poadr = pop_69/pop_20_68*100
        pai = pop_69/pop_0_14*100
        paryl = (d["Population"]*d["ex"]).sum()/total

        results.append([country,prop65,oadr,ai,aa,
                        prop_rle15,poadr,pai,paryl])

    res = pd.DataFrame(results,
        columns=["Country","Prop65+","OADR","AI","AA",
                 "PropRLE15","POADR","PAI","PARYL"])

    res.iloc[:,1:] = res.iloc[:,1:].round(2)

    cv = (res.iloc[:,1:].std()/res.iloc[:,1:].mean()*100).round(1)
    cv_row = pd.DataFrame(
        [["Coefficient of variation"] + list(cv)],
        columns=res.columns
    )

    final_table = pd.concat([res.sort_values("Country"), cv_row],
                            ignore_index=True)

    return final_table


def main():
    df = load_data("data/eu29popby1yearage.csv",
                   "data/lifeexpctancy29.csv")

    final_table = calculate_indicators(df)

    final_table.to_excel(
        "output/EU29_Turkiye_2018_Ageing_Indicators.xlsx",
        index=False
    )

    print("Analysis completed successfully.")


if __name__ == "__main__":
    main()
