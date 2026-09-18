from dataclasses import dataclass, field

records = [
    ("田中", "2026-09-01", "09:00", "18:00"),
    ("田中", "2026-09-02", "09:15", "19:45"),
    ("鈴木", "2026-09-01", "08:30", None),
    ("鈴木", "2026-09-02", "10:00", "17:30"),
    ("佐藤", "2026-09-01", "18:00", "09:00"),
    ("佐藤", "2026-09-02", None, None),
]

STANDARD_MINUTES = 480

@dataclass
class Attendance:
    name: str
    day: str
    clock_in: str | None
    clock_out: str | None

@dataclass
class DailyResult:
    name: str
    day: str
    minutes: int | None

@dataclass
class PersonSummary:
    name: str
    minutes: int = 0
    missing: int = 0
    missing_days: list[str] = field(default_factory=list)
    longest: int = 0
    overtime: int = 0

    def add(self, result: DailyResult) -> None:
        """自分の数字を1件ぶん積み上げる（自分のデータを変えるので、クラスに持たせる）"""
        # ここだけ書けました
        if result.minutes is None:
            self.missing += 1
            self.missing_days.append(result.day)
            return
        
        self.minutes += result.minutes
        self.longest = max(self.longest, result.minutes)
        self.overtime += max(0, result.minutes - STANDARD_MINUTES)

@dataclass
class Report:
    """集計結果のかたまり。PersonSummary を「持つ」（合成）。継承はしない"""
    summaries: list[PersonSummary]

    @property
    def total_minutes(self) -> int:
        return sum(person.minutes for person in self.summaries)

    @property
    def total_overtime(self) -> int:
        return sum(person.overtime for person in self.summaries)

def to_minutes(hhmm: str) -> int:
    hours, minutes = hhmm.split(":")
    return int(hours) * 60 + int(minutes)

def work_minutes(clock_in: str | None, clock_out: str | None) -> int | None:
    if clock_in is None or clock_out is None:
        return None
    start = to_minutes(clock_in)
    end = to_minutes(clock_out)
    if end < start:
        return None
    return end - start

def parse_records(rows: list[tuple[str, str, str | None, str | None]]) -> list[Attendance]:
    return [Attendance(name, day, clock_in, clock_out) for name, day, clock_in, clock_out in rows]

def evaluate(att: Attendance) -> DailyResult:
    return DailyResult(att.name, att.day, work_minutes(att.clock_in, att.clock_out))

def summarize(results: list[DailyResult]) -> Report:
    by_name: dict[str, PersonSummary] = {}
    for result in results:
        person = by_name.setdefault(result.name, PersonSummary(result.name))
        person.add(result)
    return Report(list(by_name.values()))

def format_hours(minutes: int) -> str:
    hours, rest = divmod(minutes, 60)
    return f"{hours}時間{rest:02d}分"

def format_line(person: PersonSummary) -> str:
    """表示は PersonSummary の責務ではないので、関数に渡す"""
    # ここは自分で書く（段階1の format_line を person.minutes などに置き換える）
    return ""

def render(report: Report) -> str:
    lines = ["=== 勤怠集計 ==="]
    lines += [format_line(person) for person in report.summaries]
    lines.append(f"合計: {format_hours(report.total_minutes)} / 残業 {format_hours(report.total_overtime)}")
    return "\n".join(lines)

# 1件だけの動作確認（add が単独で試せる = テストできる）
person = PersonSummary("田中")
person.add(DailyResult("田中", "2026-09-01", 540))
person.add(DailyResult("田中", "2026-09-03", None))
print(person)

report = summarize([evaluate(att) for att in parse_records(records)])
print(render(report))
