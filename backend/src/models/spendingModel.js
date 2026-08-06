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

export async function getSpendingSummary(data) {
    const [rows] = await db.execute(`
    WITH RECURSIVE main AS (
        SELECT dbc.category_name category
            ,sum(fs.bill_amount) AS total_amount
        FROM fact_spending fs
        INNER JOIN dim_bill_category dbc ON fs.bill_category_id = dbc.category_id
        GROUP BY 1
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