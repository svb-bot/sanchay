import { Grid } from "@mantine/core";

import { SummaryTable } from "../components/Dashboard";

function Dashboard() {

    return (

        <Grid>

            <Grid.Col span={{ base: 12, md: 6 }}>

                <SummaryTable
                    title="Income Summary"
                    endpoint="/dashboard/income-summary"
                />

            </Grid.Col>


            <Grid.Col span={{ base: 12, md: 6 }}>

                <SummaryTable
                    title="Spending Summary"
                    endpoint="/dashboard/spending-summary"
                />

            </Grid.Col>

        </Grid>

    );

}

export default Dashboard;