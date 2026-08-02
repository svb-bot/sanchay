import db from "../config/db.js";

export async function createPaymentMode(data) {
    const sql = `
        INSERT INTO dim_payment_mode (
            mode_name
        )
        VALUES (?)
    `;

    const [result] = await db.execute(sql, [
        data.mode_name
    ]);

    return result;
}

export async function getAllPaymentModes() {
    const [rows] = await db.execute(`
        SELECT *, mode_id AS id, mode_name AS name
        FROM dim_payment_mode
        ORDER BY mode_id
    `);

    return rows;
}

export async function getPaymentModeById(id) {
    const [rows] = await db.execute(`
        SELECT *, mode_id AS id, mode_name AS name
        FROM dim_payment_mode
        WHERE mode_id = ?
    `, [id]);

    return rows[0];
}

export async function updatePaymentMode(id, data) {
    const sql = `
        UPDATE dim_payment_mode
        SET mode_name = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE mode_id = ?
    `;

    const [result] = await db.execute(sql, [
        data.mode_name,
        id
    ]);

    return result;
}

export async function deletePaymentMode(id) {
    const sql = `
        DELETE FROM dim_payment_mode
        WHERE mode_id = ?
    `;

    const [result] = await db.execute(sql, [id]);

    return result;
}