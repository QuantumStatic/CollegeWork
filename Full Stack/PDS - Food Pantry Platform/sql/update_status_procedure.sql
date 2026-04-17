DELIMITER //

CREATE PROCEDURE UpdateOrderStatus(
    IN givenOrderID INT,
    IN username VARCHAR(255),
    IN newStatus varchar(255)
)
BEGIN
    DECLARE orderExists INT;
    
    SELECT COUNT(*)
    INTO orderExists
    FROM (
        SELECT orderId
        FROM ordered NATURAL JOIN delivered
        WHERE supervisor = username OR userName = username
    ) AS userOrders
    WHERE orderId = givenOrderID;

    -- If the OrderID exists, update the status; otherwise, throw an error
    IF orderExists > 0 THEN
        UPDATE delivered
        SET status = newStatus
        WHERE orderID = givenOrderID;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "User Does Not Have the Permission";
    END IF;
END;

//

DELIMITER ;