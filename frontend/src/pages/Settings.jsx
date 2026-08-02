import { Tabs, Stack } from "@mantine/core"

import { DimensionForm, DimensionTable } from "../components/Dimension"

import paymentCategorySchema from "../schemas/dimensions/paymentCategorySchema"
import paymentModeSchema from "../schemas/dimensions/paymentModeSchema"
import billCategorySchema from "../schemas/dimensions/billCategorySchema"
import billPaymentModeSchema from "../schemas/dimensions/billPaymentModeSchema"

function Settings() {
    return (
        <Tabs defaultValue="payment-category">
            <Tabs.List>
                <Tabs.Tab value="payment-category">Payment Categories</Tabs.Tab>

                <Tabs.Tab value="payment-mode">Payment Modes</Tabs.Tab>

                <Tabs.Tab value="bill-category">Bill Categories</Tabs.Tab>

                <Tabs.Tab value="bill-payment-mode">Bill Payment Modes</Tabs.Tab>
            </Tabs.List>

            <Tabs.Panel value="payment-category">
                <Stack mt="md">
                    <DimensionForm schema={paymentCategorySchema} />

                    <DimensionTable schema={paymentCategorySchema} />
                </Stack>
            </Tabs.Panel>

            <Tabs.Panel value="payment-mode">
                <Stack mt="md">
                    <DimensionForm schema={paymentModeSchema} />

                    <DimensionTable schema={paymentModeSchema} />
                </Stack>
            </Tabs.Panel>

            <Tabs.Panel value="bill-category" pt="md">
                <Stack>
                    <DimensionForm schema={billCategorySchema} />

                    <DimensionTable schema={billCategorySchema} />
                </Stack>
            </Tabs.Panel>

            <Tabs.Panel value="bill-payment-mode" pt="md">
                <Stack>
                    <DimensionForm schema={billPaymentModeSchema} />

                    <DimensionTable schema={billPaymentModeSchema} />
                </Stack>
            </Tabs.Panel>
        </Tabs>
    )
}

export default Settings
