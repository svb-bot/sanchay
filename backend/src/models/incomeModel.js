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
        data?.payment_notes ?? null,
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

export async function getIncomeSummary() {
    const [rows] = await db.execute(`
    WITH RECURSIVE main AS (
        SELECT 
            dpc.category_name AS category,
            SUM(fi.payment_amt) AS total_amount
        FROM fact_income fi
        JOIN dim_payment_category dpc 
        ON fi.payment_category_id = dpc.category_id
        GROUP BY dpc.category_name
    ),
    split AS (
        SELECT 
            category,
            total_amount,
            1 AS level
        FROM main

        UNION ALL

        SELECT
            s.category,
            s.total_amount,
            s.level + 1
        FROM split s
        WHERE s.level < (LENGTH(s.category) - LENGTH(REPLACE(s.category,'/',''))) + 1
    ),
    prefixes AS (
        SELECT
            SUBSTRING_INDEX(m.category, '/', s.level) AS category,
            s.total_amount
        FROM split s
        JOIN main m
        ON m.category = s.category
    )
    SELECT
        TRIM(BOTH '/' FROM category) AS category,
        SUM(total_amount) AS total_amount
    FROM prefixes
    GROUP BY 1

    UNION ALL

    SELECT
        '' AS category,
        SUM(total_amount) AS total_amount
    FROM main

    ORDER BY category
    `);
    return rows;
}