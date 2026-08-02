import { AppShell, Container, Tabs, Title, Button } from "@mantine/core"

import IncomeForm from "./forms/IncomeForm"
import SpendingForm from "./forms/SpendingForm"
import Settings from "./pages/Settings"
import { useState } from "react"
import { IconSun, IconMoon } from "@tabler/icons-react"

function App() {
    const [isDark, setIsDark] = useState(false)

    const toggleTheme = () => {
        setIsDark(!isDark)
        if (isDark) {
            document.documentElement.setAttribute("data-mantine-color-scheme", "light")
        } else {
            document.documentElement.setAttribute("data-mantine-color-scheme", "dark")
        }
    }

    return (
        <AppShell header={{ height: 60, color: "green" }} padding="md">
            <AppShell.Header color="green">
                <Container
                    h="100%"
                    style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between"
                    }}
                >
                    <Title order={3}>Sanchay</Title>
                    <Button variant="default" color="gray" size="sm" onClick={toggleTheme} title="Toggle theme">
                        {isDark ? <IconSun /> : <IconMoon />}
                    </Button>
                </Container>
            </AppShell.Header>

            <AppShell.Main>
                <Container size="lg">
                    <Tabs defaultValue="income">
                        <Tabs.List>
                            <Tabs.Tab value="income">Income</Tabs.Tab>
                            <Tabs.Tab value="spending">Spending</Tabs.Tab>
                            <Tabs.Tab value="settings">Settings</Tabs.Tab>
                        </Tabs.List>

                        <Tabs.Panel value="income" pt="md">
                            <IncomeForm />
                        </Tabs.Panel>

                        <Tabs.Panel value="spending" pt="md">
                            <SpendingForm />
                        </Tabs.Panel>

                        <Tabs.Panel value="settings" pt="md">
                            <Settings />
                        </Tabs.Panel>
                    </Tabs>
                </Container>
            </AppShell.Main>
        </AppShell>
    )
}

export default App
