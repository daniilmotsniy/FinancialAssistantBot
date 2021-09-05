import React from 'react'
import {Bar} from 'react-chartjs-2';
import {gql, useQuery} from "@apollo/client";

const ASSET_COUNT = gql`
  query AssetCount($asset: String!) {
    assetCount(asset: $asset) {
      label
      count
    }
  }
`;

function Asset({asset, color}) {
    const { loading, error, data } = useQuery(ASSET_COUNT,{
        variables: {asset: asset},
    })
    if (loading) return <p>Loading...</p>
    if (error) return <p>${error}</p>

    let new_label = asset.split('_')[1]
    new_label = new_label[0].toUpperCase() + new_label.slice(1)

    let state = {
        labels: data.assetCount.map(({ label, _ }) => (label)),
        datasets: [
            {
                label: new_label,
                backgroundColor: color,
                borderColor: 'rgb(70,70,70)',
                borderWidth: 2,
                data: data.assetCount.map(({ _, count }) => (count))
            }
        ]
    }

    return (
        <div>
            <Bar
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

export default Asset