set $i = 0
set $end = 65
set $current = $rcx
while ($i++ < $end)
    printf "%02x", *(unsigned char *)($current)
    set $current = $current + 1
end