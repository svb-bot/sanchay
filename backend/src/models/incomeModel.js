import db from "../config/db.js";

export async function createIncome(data) {
    const sql = `
        INSERT INTO fact_income (
            payment_date,
            payment_category_id,
            payment_payee_name,
            payment_amt,
            payment_mode_id,
            payment_notes
        )
        VALUES (?, ?, ?, ?, ?, ?)
    `;

    const [result] = await db.execute(sql, [
        data.payment_date,
        data.payment_category_id,
        data.payment_payee_name,
        data.payment_amt,
        data.payment_mode_id,
        data.payment_notes
    ]);

    return result;
}

export async function getAllIncome() {
    const [rows] = await db.execute(`
        SELECT *
        FROM fact_income
        ORDER BY payment_date DESC, payment_id DESC
    `);

    return rows;
}