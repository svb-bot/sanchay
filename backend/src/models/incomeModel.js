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
    WITH main AS (
        SELECT dpc.category_name category
            ,sum(fi.payment_amt) AS total_amount
        FROM fact_income fi
        INNER JOIN dim_payment_category dpc ON fi.payment_category_id = dpc.category_id
        GROUP BY 1
    ),
    split_1 AS (
        SELECT CONCAT (SUBSTRING_INDEX(category, '/', 1)) category
            ,total_amount
        FROM main
        WHERE category LIKE '%/%'
    ),
    split_2 AS (
        SELECT CONCAT (
                SUBSTRING_INDEX(category, '/', 1)
                ,'/'
                ,SUBSTRING_INDEX(SUBSTRING_INDEX(category, '/', 2), '/', - 1)
                ) category
            ,total_amount
        FROM main
        WHERE category LIKE '%/%/%'
    )
    SELECT *
    FROM (
        SELECT category
            ,total_amount
        FROM main
        
        UNION ALL
        
        SELECT category
            ,sum(total_amount) total_amount
        FROM split_1
        GROUP BY 1
        
        UNION ALL
        
        SELECT category
            ,sum(total_amount) total_amount
        FROM split_2
        GROUP BY 1
    ) a
    ORDER BY 1

    `);
    return rows;
}