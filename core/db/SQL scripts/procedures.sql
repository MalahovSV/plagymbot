CREATE OR REPLACE PROCEDURE set_telegram_id_for_user(
    p_user_id INTEGER,
    p_telegram_id BIGINT
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE users
    SET telegram_id = p_telegram_id
    WHERE id = p_user_id;

    -- Опционально: проверить, был ли обновлён хотя бы один ряд
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Пользователь с id=% не найден', p_user_id;
    END IF;
END;
$$;