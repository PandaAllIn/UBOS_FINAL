PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- ============================================================
-- Core intelligence tables
-- ============================================================

CREATE TABLE IF NOT EXISTS grants (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    program TEXT,
    deadline TEXT,
    budget REAL,
    fit_score REAL,
    status TEXT DEFAULT 'new',
    source_mission TEXT,
    discovered_at TEXT,
    tags TEXT DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS insights (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    summary TEXT NOT NULL,
    details TEXT,
    source TEXT,
    source_mission TEXT,
    discovered_at TEXT,
    relevance_score REAL,
    tags TEXT DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS contacts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    organization TEXT,
    role TEXT,
    connection_strength TEXT,
    location TEXT,
    last_contact TEXT,
    tags TEXT DEFAULT '[]',
    notes TEXT,
    source_mission TEXT,
    discovered_at TEXT
);

CREATE TABLE IF NOT EXISTS revenue_signals (
    id TEXT PRIMARY KEY,
    channel TEXT,
    value_estimate REAL,
    probability REAL,
    stage TEXT,
    source_mission TEXT,
    created_at TEXT,
    tags TEXT DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS operational_metrics (
    id TEXT PRIMARY KEY,
    metric_type TEXT NOT NULL,
    value REAL,
    timestamp TEXT,
    source_mission TEXT
);

-- ============================================================
-- Indexes
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_grants_deadline ON grants(deadline);
CREATE INDEX IF NOT EXISTS idx_grants_fit_score ON grants(fit_score);
CREATE INDEX IF NOT EXISTS idx_grants_status ON grants(status);

CREATE INDEX IF NOT EXISTS idx_insights_category ON insights(category);
CREATE INDEX IF NOT EXISTS idx_insights_relevance ON insights(relevance_score);

CREATE INDEX IF NOT EXISTS idx_contacts_location ON contacts(location);
CREATE INDEX IF NOT EXISTS idx_contacts_connection ON contacts(connection_strength);

CREATE INDEX IF NOT EXISTS idx_revenue_stage ON revenue_signals(stage);
CREATE INDEX IF NOT EXISTS idx_revenue_probability ON revenue_signals(probability);

CREATE INDEX IF NOT EXISTS idx_operational_metric_type ON operational_metrics(metric_type);
CREATE INDEX IF NOT EXISTS idx_operational_timestamp ON operational_metrics(timestamp);

-- ============================================================
-- Full-text search virtual tables
-- ============================================================

CREATE VIRTUAL TABLE IF NOT EXISTS grants_fts USING fts5(
    title,
    program,
    tokenize='porter',
    content='grants',
    content_rowid='rowid'
);

CREATE VIRTUAL TABLE IF NOT EXISTS insights_fts USING fts5(
    summary,
    details,
    tokenize='porter',
    content='insights',
    content_rowid='rowid'
);

CREATE VIRTUAL TABLE IF NOT EXISTS contacts_fts USING fts5(
    name,
    organization,
    role,
    notes,
    tokenize='porter',
    content='contacts',
    content_rowid='rowid'
);

CREATE VIRTUAL TABLE IF NOT EXISTS revenue_signals_fts USING fts5(
    channel,
    stage,
    tokenize='porter',
    content='revenue_signals',
    content_rowid='rowid'
);

CREATE VIRTUAL TABLE IF NOT EXISTS operational_metrics_fts USING fts5(
    metric_type,
    tokenize='porter',
    content='operational_metrics',
    content_rowid='rowid'
);

-- ============================================================
-- FTS maintenance triggers
-- ============================================================

CREATE TRIGGER IF NOT EXISTS grants_ai AFTER INSERT ON grants BEGIN
    INSERT INTO grants_fts(rowid, title, program) VALUES (new.rowid, new.title, new.program);
END;

CREATE TRIGGER IF NOT EXISTS grants_ad AFTER DELETE ON grants BEGIN
    INSERT INTO grants_fts(grants_fts, rowid, title, program) VALUES ('delete', old.rowid, old.title, old.program);
END;

CREATE TRIGGER IF NOT EXISTS grants_au AFTER UPDATE ON grants BEGIN
    INSERT INTO grants_fts(grants_fts, rowid, title, program) VALUES ('delete', old.rowid, old.title, old.program);
    INSERT INTO grants_fts(rowid, title, program) VALUES (new.rowid, new.title, new.program);
END;

CREATE TRIGGER IF NOT EXISTS insights_ai AFTER INSERT ON insights BEGIN
    INSERT INTO insights_fts(rowid, summary, details) VALUES (new.rowid, new.summary, new.details);
END;

CREATE TRIGGER IF NOT EXISTS insights_ad AFTER DELETE ON insights BEGIN
    INSERT INTO insights_fts(insights_fts, rowid, summary, details) VALUES ('delete', old.rowid, old.summary, old.details);
END;

CREATE TRIGGER IF NOT EXISTS insights_au AFTER UPDATE ON insights BEGIN
    INSERT INTO insights_fts(insights_fts, rowid, summary, details) VALUES ('delete', old.rowid, old.summary, old.details);
    INSERT INTO insights_fts(rowid, summary, details) VALUES (new.rowid, new.summary, new.details);
END;

CREATE TRIGGER IF NOT EXISTS contacts_ai AFTER INSERT ON contacts BEGIN
    INSERT INTO contacts_fts(rowid, name, organization, role, notes) VALUES (new.rowid, new.name, new.organization, new.role, new.notes);
END;

CREATE TRIGGER IF NOT EXISTS contacts_ad AFTER DELETE ON contacts BEGIN
    INSERT INTO contacts_fts(contacts_fts, rowid, name, organization, role, notes) VALUES ('delete', old.rowid, old.name, old.organization, old.role, old.notes);
END;

CREATE TRIGGER IF NOT EXISTS contacts_au AFTER UPDATE ON contacts BEGIN
    INSERT INTO contacts_fts(contacts_fts, rowid, name, organization, role, notes) VALUES ('delete', old.rowid, old.name, old.organization, old.role, old.notes);
    INSERT INTO contacts_fts(rowid, name, organization, role, notes) VALUES (new.rowid, new.name, new.organization, new.role, new.notes);
END;

CREATE TRIGGER IF NOT EXISTS revenue_ai AFTER INSERT ON revenue_signals BEGIN
    INSERT INTO revenue_signals_fts(rowid, channel, stage) VALUES (new.rowid, new.channel, new.stage);
END;

CREATE TRIGGER IF NOT EXISTS revenue_ad AFTER DELETE ON revenue_signals BEGIN
    INSERT INTO revenue_signals_fts(revenue_signals_fts, rowid, channel, stage) VALUES ('delete', old.rowid, old.channel, old.stage);
END;

CREATE TRIGGER IF NOT EXISTS revenue_au AFTER UPDATE ON revenue_signals BEGIN
    INSERT INTO revenue_signals_fts(revenue_signals_fts, rowid, channel, stage) VALUES ('delete', old.rowid, old.channel, old.stage);
    INSERT INTO revenue_signals_fts(rowid, channel, stage) VALUES (new.rowid, new.channel, new.stage);
END;

CREATE TRIGGER IF NOT EXISTS operational_ai AFTER INSERT ON operational_metrics BEGIN
    INSERT INTO operational_metrics_fts(rowid, metric_type) VALUES (new.rowid, new.metric_type);
END;

CREATE TRIGGER IF NOT EXISTS operational_ad AFTER DELETE ON operational_metrics BEGIN
    INSERT INTO operational_metrics_fts(operational_metrics_fts, rowid, metric_type) VALUES ('delete', old.rowid, old.metric_type);
END;

CREATE TRIGGER IF NOT EXISTS operational_au AFTER UPDATE ON operational_metrics BEGIN
    INSERT INTO operational_metrics_fts(operational_metrics_fts, rowid, metric_type) VALUES ('delete', old.rowid, old.metric_type);
    INSERT INTO operational_metrics_fts(rowid, metric_type) VALUES (new.rowid, new.metric_type);
END;
