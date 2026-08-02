import db from "../config/db.js";

export async function createBillCategory(data) {
    const sql = `
        INSERT INTO dim_bill_category (
            category_name
        )
        VALUES (?)
    `;

    const [result] = await db.execute(sql, [
        data.category_name
    ]);

    return result;
}

export async function getAllBillCategories() {
    const [rows] = await db.execute(`
        SELECT *, category_id AS id, category_name AS name
        FROM dim_bill_category
        ORDER BY category_id
    `);

    return rows;
}

export async function getBillCategoryById(id) {
    const [rows] = await db.execute(`
        SELECT *, category_id AS id, category_name AS name
        FROM dim_bill_category
        WHERE category_id = ?
    `, [id]);

    return rows;
}

export async function updateBillCategory(id, data) {
    const sql = `
        UPDATE dim_bill_category
        SET category_name = ?
        WHERE category_id = ?
    `;

    const [result] = await db.execute(sql, [
        data.category_name,
        id
    ]);

    return result;
}

export async function deleteBillCategory(id) {
    const sql = `
        DELETE FROM dim_bill_category
        WHERE category_id = ?
    `;

    const [result] = await db.execute(sql, [id]);

    return result;
}