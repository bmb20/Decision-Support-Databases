SELECT COUNT(*)
FROM Custody
JOIN Date ON Custody.date_fk = Date.date_pk
JOIN Geography ON Custody.geo_id = Geography.geo_id
JOIN Participant ON Custody.participant_id = Participant.participant_id
JOIN Gun ON Custody.gun_id = Gun.gun_id