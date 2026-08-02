import db from "../config/db.js";

export async function createSpending(data) {
    const sql = `
        INSERT INTO fact_spending (
            bill_date,
            bill_category_id,
            bill_issuer_name,
            bill_amount,
            bill_reference,
            bill_payment_mode_id,
            bill_notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    `;

    const [result] = await db.execute(sql, [
        data.bill_date,
        data.bill_category_id,
        data.bill_issuer_name,
        data.bill_amount,
        data.bill_reference,
        data.bill_payment_mode_id,
        data.bill_notes
    ]);

    return result;
}

export async function getAllSpending() {
    const [rows] = await db.execute(`
        SELECT *
        FROM fact_spending
        ORDER BY bill_date DESC, payment_id DESC
    `);

    return rows;
}