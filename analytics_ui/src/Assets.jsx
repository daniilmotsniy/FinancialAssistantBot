import React from 'react'
import {Pie} from 'react-chartjs-2';
import {gql, useQuery} from "@apollo/client";
import {chartColors} from "./colors";

const ASSETS_COUNT = gql`
  query AssetsCount {
   assetsCount {
     userStocks
     userCurrencies
     userCryptos
     userResources
   }
  }
`;

function Assets() {
    const { loading, error, data } = useQuery(ASSETS_COUNT)

    if (loading) return <p>Loading...</p>
    if (error) return <p>${error}</p>

    let state = {
        labels: Object.keys(data.assetsCount),
        datasets: [
            {
                label: 'Total count of assets',
                backgroundColor: chartColors,
                borderColor: 'rgb(70,70,70)',
                borderWidth: 2,
                data: Object.values(data.assetsCount)
            }
        ]
    }

    return (
        <div>
            <Pie
                data={state}
                options={{
                    title:{
                        display:true,
                        fontSize:20
                    },
                    legend:{
                        display:true,
                        position:'right'
                    }
                }}
            />
        </div>
    )
}

export default Assets