import db from "../config/db.js";

export async function createPaymentCategory(data) {
    const sql = `
        INSERT INTO dim_payment_category (
            category_name
        )
        VALUES (?)
    `;

    console.log(data)
    const [result] = await db.execute(sql, [
        data.category_name
    ]);

    return result;
}

export async function getAllPaymentCategories() {
    const [rows] = await db.execute(`
        SELECT *, category_id AS id, category_name AS name
        FROM dim_payment_category
        ORDER BY category_id
    `);

    return rows;
}

export async function getPaymentCategoryById(id) {
    const [rows] = await db.execute(`
        SELECT *, category_id AS id, category_name AS name
        FROM dim_payment_category
        WHERE category_id = ?
    `, [id]);

    return rows[0];
}

export async function updatePaymentCategory(id, data) {
    const sql = `
        UPDATE dim_payment_category
        SET category_name = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE category_id = ?
    `;

    const [result] = await db.execute(sql, [
        data.category_name,
        id
    ]);

    return result;
}

export async function deletePaymentCategory(id) {
    const sql = `
        DELETE FROM dim_payment_category
        WHERE category_id = ?
    `;

    const [result] = await db.execute(sql, [id]);

    return result;
}