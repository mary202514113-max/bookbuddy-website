import re

path = "book.html"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

out_lines = []
for line in lines:
    if "status:'coming_soon'" in line:
        # Extract book id from line like 'book-002': { id:'book-002', ...
        m = re.search(r"'(book-\d{3})':", line)
        if m:
            bid = m.group(1)
            line = line.replace("status:'coming_soon'", "status:'online', video:'books/{}/video_uk.mp4'".format(bid))
    out_lines.append(line)

with open(path, "w", encoding="utf-8") as f:
    f.writelines(out_lines)

print("Done: updated coming_soon books to online + added video field")
