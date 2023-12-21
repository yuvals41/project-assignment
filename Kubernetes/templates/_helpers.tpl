{{- define "app.image" -}}
{{- $registryName := .Values.deployment.image.registry -}}
{{- $repositoryName := .Values.deployment.image.repository | default .Chart.Name -}}
{{- $tag := .Values.deployment.image.tag | default .Chart.AppVersion | default .Chart.Version -}}
{{- printf "%s/%s:%s" $registryName $repositoryName $tag -}}
{{- end -}}

