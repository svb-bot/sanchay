import {
    AppShell,
    Container,
    Tabs,
    Title
} from "@mantine/core";

import IncomeForm from "./forms/IncomeForm";
import SpendingForm from "./forms/SpendingForm";
import Settings from "./pages/Settings";


function App() {

    return (
        <AppShell
            header={{ height: 60 }}
            padding="md"
        >

            <AppShell.Header>

                <Container
                    h="100%"
                    style={{
                        display: "flex",
                        alignItems: "center"
                    }}
                >
                    <Title order={3}>
                        Sanchay
                    </Title>

                </Container>

            </AppShell.Header>


            <AppShell.Main>

                <Container size="lg">

                    <Tabs defaultValue="income">

                        <Tabs.List>

                            <Tabs.Tab value="income">
                                Income
                            </Tabs.Tab>


                            <Tabs.Tab value="spending">
                                Spending
                            </Tabs.Tab>


                            <Tabs.Tab value="settings">
                                Settings
                            </Tabs.Tab>

                        </Tabs.List>



                        <Tabs.Panel
                            value="income"
                            pt="md"
                        >
                            <IncomeForm />
                        </Tabs.Panel>



                        <Tabs.Panel
                            value="spending"
                            pt="md"
                        >
                            <SpendingForm />
                        </Tabs.Panel>



                        <Tabs.Panel
                            value="settings"
                            pt="md"
                        >
                            <Settings />
                        </Tabs.Panel>


                    </Tabs>

                </Container>

            </AppShell.Main>

        </AppShell>
    );
}


export default App;